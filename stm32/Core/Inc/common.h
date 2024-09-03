/*
 * common.h
 *
 *  Created on: Jul 7, 2024
 *      Author: nkenn
 */

#ifndef INC_COMMON_H_
#define INC_COMMON_H_

#include <stdint.h>   // Include standard integer types

// Define the buffer size as a constant
// Define the buffer size as a constant
#define COM_BUFFER_SIZE 6

// Declare the buffers as extern, so they can be used in other files
extern uint8_t rx_buffer[COM_BUFFER_SIZE];
extern uint8_t tx_buffer[COM_BUFFER_SIZE];

// Declare com_buffer_size as extern
extern uint8_t com_buffer_size;

#endif /* INC_COMMON_H_ */
