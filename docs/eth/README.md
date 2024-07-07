We will use the LAN8720 ETH Board for this project:

https://www.waveshare.com/w/upload/1/1a/LAN8720A.pdf

STM32 Setup:

1. Enable ETH in "RMII mode"
2. Include Software/Middleware "LWIP"
3. In LWIP Settings:  
   1. General Settings:
      1. Disable LWIP_DHCP
      2. Set IP Address 192.168.000.010
      3. Set Netmask 255.255.255.0
      4. Set Gateway address 192.168.000.001
      5. Note: Make sure this does not conflict with your current network!
   2. Platform Settings
      1. IPs or Components -> LAN8742
      2. Found Solutions -> LAN8742

PC Setup (Windows):
1. Control panel -> Network Connections
2. Right click the adapter for this PC
   1. Properties
      1. Internet Protocol Version 4 (TCP/IPv4)
         1. Use the following IP address
            1. IP address: 192.168.0.20
            2. Subnet Mask: 255.255.255.0

Connect the Pins of the LAN8720 Board Using the pinout shown in config

Build and flash the firmware to stm32 (run button in stm32CubeIDE)

Open a terminal and verify 

ping 192.168.0.10 -> shoudl return!

