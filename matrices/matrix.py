#!/usr/bin/env python

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import sys
import time


class RunText:
    def __init__(self, *args, **kwargs):
        # Create an RGBMatrix object
        self.matrix = RGBMatrix(options = self.getOptions())


    def getOptions(self) -> RGBMatrixOptions:
        """Create and set an RGBMatrixOptions object

        Returns:
            RGBMatrixOptions
        """        

        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 100
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.panel_type = ""

        return options

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("data/karma2.bdf")
        textColor = graphics.Color(255,0,0)
        pos = offscreen_canvas.width
        my_text = "SELF-DRIVING // SELF-DRIVING // SELF-DRIVING // SELF-DRIVING"

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 26, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.01)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def process(self):
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True


# Main function
if __name__ == "__main__":
    run_text = RunText()

    # Start the program in a loop
    # Stop on keyboard interrupt
    run_text.process()
