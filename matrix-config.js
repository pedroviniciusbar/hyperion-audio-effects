var width = 23
var height = 13

var index = 0

var leds = []

var hblock = 1.0 / width
var vblock = 1.0 / height

var x, y

function addLed (index, x, y) {
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

// Snake from bottom right
for (y = height - 1; y >= 0; --y) {
  if (y % 2 === 0) {
    // Right-to-left
    for (x = width - 1; x >= 0; --x) {
      addLed(index, x, y)
      index++
    }
  } else {
    // Left-to-right
    for (x = 0; x < width; ++x) {
      addLed(index, x, y)
      index++
    }
  }
}

console.log(JSON.stringify(leds, function (key, val) {
  // Float precision
  return val.toFixed ? Number(val.toFixed(4)) : val
}, 2))
