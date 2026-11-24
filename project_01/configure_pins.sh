#!/bin/bash
# configure_pins.sh
config-pin P1_06 spi_cs
config-pin P1_08 spi_sclk
config-pin P1_12 spi_d0
# plus any gpio pins your buttons/LED/buzzer need, e.g.:
# config-pin P2_02 gpio