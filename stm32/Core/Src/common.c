/*
 * common.c
 *
 *  Created on: Sep 3, 2024
 *      Author: nkenn
 */


#include "common.h"

// Define the buffers with the specified size
uint8_t rx_buffer[MAX_COM_BUFFER_SIZE];
uint8_t tx_buffer[MAX_COM_BUFFER_SIZE];

// Define and initialize com_buffer_size
uint8_t com_buffer_size = MAX_COM_BUFFER_SIZE;

