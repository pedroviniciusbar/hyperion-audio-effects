/**
 * Node.js based configurator for led matrices to be used with Hyperion
 *
 * MIT License
 * Copyright (c) 2016 RanzQ (Juha Rantanen)
 */

var parallel = false
var width = 32
var height = 8
var start = 'bottom-right'
var debug = false

var index = 0

var leds = []

var hblock = 1.0 / width
var vblock = 1.0 / height

// var hmin = 999.0
// var hmax = -999.0
// var vmin = 999.0
// var vmax = -999.0

/**
 * Adds led to the hyperion config led array
 * @param {Number} index Index of the led
 * @param {Number} x     Horizontal position in matrix
 * @param {Number} y     Vertical position in matrix
 */
function addLed (index, x, y) {
  // if (debug) console.log(index + ':', x + ',', y)
  var hscanMin = x * hblock
  var hscanMax = (x + 1) * hblock
  var vscanMin = y * vblock
  var vscanMax = (y + 1) * vblock

  // These were used for debug
  // if (hscanMin < hmin) hmin = hscanMin
  // if (hscanMax > hmax) hmax = hscanMax
  // if (vscanMin < vmin) vmin = vscanMin
  // if (vscanMax > vmax) vmax = vscanMax

  leds.push({
    index: index,
    hscan: {
      minimum: hscanMin,
      maximum: hscanMax
    },
    vscan: {
      minimum: vscanMin,
      maximum: vscanMax
    }
  })
}

/**
 * Print help text
 * @return {undefined}
 */
function printHelp () {
  console.log('Hyperion matrix configurator by RanzQ')
  console.log('-------------------------------------')
  console.log('options:')
  console.log('-w --width <number>        : Matrix width')
  console.log('-h --height <number>       : Matrix height')
  console.log('-p --parallel              : Parallel rows (not snake)')
  console.log('-s --start [ver]-[hor]     : Starting corner, e.g. top-right')
  console.log('-d --debug                 : Debug print instead of json output')
  process.exit(0)
}

try {
  var widthNext, heightNext, startNext

  process.argv.forEach(function (val, index, array) {
    if (widthNext) {
      width = parseInt(val, 10)
      hblock = 1.0 / width
      widthNext = false
      return
    } else if (heightNext) {
      height = parseInt(val, 10)
      vblock = 1.0 / height
      heightNext = false
      return
    } else if (startNext) {
      start = val
      startNext = false
      return
    }

    switch (val) {
      case '-p':
      case '--parallel':
        parallel = true
        break
      case '-w':
      case '--width':
        widthNext = true
        break
      case '-h':
      case '--height':
        heightNext = true
        break
      case '-s':
      case '--start':
        startNext = true
        break
      case '-d':
      case '--debug':
        debug = true
        break
      case 'help':
      case '--help':
        printHelp()
        break
      default:
        break
    }
  })

  var startYX = start.split('-')
  var startX = startYX[1] === 'right' ? width - 1 : 0
  var startY = startYX[0] === 'bottom' ? height - 1 : 0
  var endX = startX === 0 ? width - 1 : 0
  var endY = startY === 0 ? height - 1 : 0

  var forward = startX < endX

  var downward = startY < endY

  var debugMatrix = new Array(height)
  for (var i = 0; i < height; i++) {
    debugMatrix[i] = new Array(width)
  }

  var x, y

  for (y = startY; downward && y <= endY || !downward && y >= endY; y += downward ? 1 : -1) {
    for (x = startX; forward && x <= endX || !forward && x >= endX; x += forward ? 1 : -1) {
      addLed(index, x, y)
      if (debug) debugMatrix[y][x] = index
      index++
    }
    if (!parallel) {
      forward = !forward
      var tmp = startX
      startX = endX
      endX = tmp
    }
  }

  if (debug) {
    var debugStr = ''
    for (i = 0; i < debugMatrix.length; i++) {
      for (var j = 0; j < debugMatrix[i].length; j++) {
        var idx = debugMatrix[i][j]
        if (idx == null) idx = '   '
        else if (idx < 10) idx = '  ' + idx
        else if (idx < 100) idx = ' ' + idx
        debugStr += '[' + idx + ']'
      }
      debugStr += '\n'
    }
    console.log(debugStr)
    // console.log('------------')
    // console.log('hmin:', hmin)
    // console.log('hmax:', hmax)
    // console.log('vmin:', vmin)
    // console.log('vmax:', vmax)
  }
} catch (e) {
  console.error('Invalid arguments:', e)
  process.exit(0)
}

if (!debug) {
  console.log(JSON.stringify({leds: leds}, function (key, val) {
    // Float precision
    return val.toFixed ? Number(val.toFixed(4)) : val
  }, 2))
}

