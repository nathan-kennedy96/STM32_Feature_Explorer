/*
 * command_manager.c
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */

#include "command_manager.h"
#include "rtc_manager.h"

FunctionPointer function_map[NUM_FUNCTIONS];
Message rx_message;

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

void get_time(Message* rx_msg, uint8_t* tx_buffer){
	//If a timestamp is sent -> we update the rtc clock
	if (rx_msg->data != 0){
		set_rtc_from_timestamp(rx_msg->data);
	}
	const Message ret_msg = {
	        .cmd = TIME,
	        .data = get_rtc_seconds_since_epoch(),
	};
	serialize_message(&ret_msg, tx_buffer);
}


// Initialization function for the command map
void initialize_function_map(void) {
    function_map[NOK] = nok;
    function_map[HELLO] = hello;
    function_map[TIME] = get_time;
}

void handle_request(const uint8_t* rx_buffer, uint8_t* tx_buffer){
	deserialize_message(rx_buffer, &rx_message); //TODO: handle deserialization failures and unknown msgs!
	// We should use the NOK return for those!
	function_map[rx_message.cmd](&rx_message, tx_buffer);
}
