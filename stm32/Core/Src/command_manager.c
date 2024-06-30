/*
 * command_manager.c
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */

#include "command_manager.h"

FunctionPointer function_map[NUM_FUNCTIONS];

void nok(Message* rx_msg, uint8_t* tx_buffer){
	// Respond with all zeros
	const Message ret_msg = {
		.cmd = NOK,
		.data = 0
	};
	serialize_message(&ret_msg, tx_buffer);
}

void hello(Message* rx_msg, uint8_t* tx_buffer){
	//For now we will just have hello respond their number + 1
	const Message ret_msg = {
	        .cmd = HELLO,
	        .data = rx_msg->data + 1
	};
	serialize_message(&ret_msg, tx_buffer);
}

// Initialization function for the command map
void initialize_function_map(void) {
    function_map[NOK] = nok;
    function_map[HELLO] = hello;
}
