/**
 * None of this is actually used at the moment in the frontend code!
 * We may come back to this code as a reference especially for handling color
 * selection
 */

let color = '#FFF';
let strokeWidth = 4;
let socket;

function setup() {
	// Creating canvas
	const cv = createCanvas(800, 600)
	cv.position(600, 100)
  cv.background(0)

	// Getting our buttons and the holder through the p5.js dom
	const color_picker = select('#pickcolor')
	const color_btn = select('#color-btn')
	const color_holder = select('#color-holder')

	const stroke_width_picker = select('#stroke-width-picker')
	const stroke_btn = select('#stroke-btn')

	// Adding a mousePressed listener to the button
	color_btn.mousePressed(() => {
		// Checking if the input is a valid hex color
		if (/(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)/i.test(color_picker.value())) {
			color = color_picker.value()
			color_holder.style('background-color', color)
		}
		else {console.log('Enter a valid hex value')}
	})

	// Adding a mousePressed listener to the button
	stroke_btn.mousePressed(() => {
		const width = parseInt(stroke_width_picker.value())
		if (width > 0) strokeWidth = width
	})
}

function mouseDragged() {
	// Draw
	stroke(color)
	strokeWeight(strokeWidth)
  line(mouseX, mouseY, pmouseX, pmouseY)
  
  // send the mouse coords
  sendmouse(mouseX, mouseY, pmouseX, pmouseY)
}