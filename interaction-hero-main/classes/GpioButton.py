class GpioButton():
    # Requires a gpio_zero Button object as argument!
    # https://gpiozero.readthedocs.io/en/stable/api_input.html#button
    def __init__(self, gpio_bt_obj):
        self.gpiozero_button_object = gpio_bt_obj

        # grab gpio pin number from gpio_zero object and cast to int
        self.gpio_key = int(str(self.gpiozero_button_object.pin)[4:])
        self.available = True
    
    def is_available(self):
        return self.available

    def wake(self):
        self.available = True

    def is_pressed(self):
        return self.gpiozero_button_object.is_pressed

    def use(self):
        self.available = False