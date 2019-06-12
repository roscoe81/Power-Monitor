# Power-Monitor
This project uses a Raspberry Pi to send Pushover alerts when a mains power failure occurs. It requires a UPS to supply power to the Raspberry Pi so that it continues to be powered during a mains power failure. A non-UPS backed up power outlet is used to monitor the mains power availability through an off-the-shelf 5V plug pack. A typical use case for this project is to monitor the mains power that's being supplied to a boat while berthed at a marina. Given that the boat has its own inverter, it provides the necessary UPS capability and alerts the owner or the marina operator to restore power before the boat's batteries are depleted.

A pushover alert is sent immediately upon a mains power failure. The user can set the elapsed time (in hours) at which an initial pushover reminder of the power failure duration is sent, as well as the frequency of subsequent reminders. A pushover alert is sent when power is restored.

## Hardware Schematic
![Schematic](https://github.com/roscoe81/Power-Monitor/blob/master/Power_Monitor_Schem.png)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
