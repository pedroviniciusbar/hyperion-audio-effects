var parallel = false
var width = 32
var height = 8
var start = 'bottom-right'
var debug = false

var index = 0

var leds = []

var hblock = 1.0 / width
var vblock = 1.0 / height

function addLed (index, x, y) {
  if (debug) console.log(index + ':', x + ',', y)
  leds.push({
    index: index,
    hscan: {
      minimum: x * hblock,
      maximum: (x + 1) * hblock
    },
    vscan: {
      minimum: y * vblock,
      maximum: (y + 1) * vblock
    }
  })
}

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
      widthNext = false
      return
    } else if (heightNext) {
      height = parseInt(val, 10)
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
  var endX = startX === 0 ? width : -1
  var endY = startY === 0 ? height : -1
  var growX = startX === 0 ? 1 : -1
  var growY = startY === 0 ? 1 : -1

  var evenY = height % 2 === 0

  var x, y

  for (y = startY; y !== endY; y += growY) {
    if (parallel || evenY && y % 2 === 0 || !evenY && y % 2 === 1) {
      // Forward
      if (debug) console.log('\ni: x, y (forward)\n------')
      for (x = startX; x !== endX; x += growX) {
        addLed(index, x, y)
        index++
      }
    } else if (!parallel) {
      // Backward
      if (debug) console.log('\ni: x, y (backward)\n------')
      for (x = endX - growX; x !== startX - growX; x -= growX) {
        addLed(index, x, y)
        index++
      }
    }
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

