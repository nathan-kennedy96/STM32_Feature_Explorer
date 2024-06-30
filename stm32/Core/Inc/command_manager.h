/*
 * command_manager.h
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */

#ifndef INC_COMMAND_MANAGER_H_
#define INC_COMMAND_MANAGER_H_

#include "message.h"
#include "stm32f4xx_hal.h"

// Define a function pointer type for command functions
typedef void (*FunctionPointer)(Message*, uint8_t*);

// Declare the number of functions in the function map
#define NUM_FUNCTIONS 2

// Declare the function map array
extern FunctionPointer function_map[NUM_FUNCTIONS];

// Function prototypes for the command handling functions
void nok(Message* rx_msg, uint8_t* tx_buffer);
void hello(Message* rx_msg, uint8_t* tx_buffer);

// Initialization function for the command map
void initialize_function_map(void);

#endif /* INC_COMMAND_MANAGER_H_ */
