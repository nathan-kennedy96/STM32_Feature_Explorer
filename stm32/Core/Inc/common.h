/*
 * common.h
 *
 *  Created on: Jul 7, 2024
 *      Author: nkenn
 */

#ifndef INC_COMMON_H_
#define INC_COMMON_H_

#include <stdint.h>   // Include standard integer types

#define COMM_BUFFER_SIZE 4


extern uint8_t rx_buffer[COMM_BUFFER_SIZE];
extern uint8_t tx_buffer[COMM_BUFFER_SIZE];

#endif /* INC_COMMON_H_ */
