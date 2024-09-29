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


// Function to handle NOK command
void nok(Message* rx_msg, uint8_t* tx_buffer) {
    // Create the return message header for NOK
    const MessageHeader ret_msg_hdr = {
        .command = NOK,         // NOK command
        .payload_size = 1       // Payload size: 1 byte
    };

    // Create the return message and allocate memory for its payload
    Message ret_msg = {
        .header = ret_msg_hdr,
        .data = malloc(1 * sizeof(uint8_t))  // Allocate memory for 1 byte of payload
    };

    if (!ret_msg.data) {
        printf("Failed to allocate memory for response payload\n");
        return;
    }

    // Set the payload to a single byte of 0
    uint8_t* tx_data = (uint8_t*)ret_msg.data;  // Cast payload to uint8_t*
    tx_data[0] = 0;  // Set the single byte payload to 0

    // Serialize the response message into the tx_buffer
    serialize_message(&ret_msg, tx_buffer);

    // Free the dynamically allocated memory for the response payload
    free(ret_msg.data);
}

void hello(Message* rx_msg, uint8_t* tx_buffer){
	//Hello response with +1 added to each element
	const MessageHeader ret_msg_hdr = {
	        .command = HELLO,
	        .payload_size = rx_msg->header.payload_size,
	};

	// Allocate memory for the response message
    Message ret_msg = {
        .header = ret_msg_hdr,
        .data = malloc(rx_msg->header.payload_size * sizeof(uint16_t))
    };

	    // Process the received message's payload (assume uint16_t payload)
    uint16_t* rx_data = (uint16_t*)rx_msg->data;  // Cast the received message payload
    uint16_t* tx_data = (uint16_t*)ret_msg.data;  // Cast the response message payload

    for (size_t i = 0; i < rx_msg->header.payload_size; i++) {
        tx_data[i] = rx_data[i] + 1;  // Add 1 to each element
    }

	serialize_message(&ret_msg, tx_buffer);

	 // Free the allocated memory for the response payload
    free(ret_msg.data);
}

void get_time(Message* rx_msg, uint8_t* tx_buffer){
	//If a timestamp is sent -> we update the rtc clock
	if (rx_msg->data != NULL) {
        uint32_t* timestamp = (uint32_t*)rx_msg->data;
        set_rtc_from_timestamp(*timestamp);  // Update the RTC with the provided timestamp
    }

	// Create the return message with the current RTC time
    uint32_t current_time = get_rtc_seconds_since_epoch();  // Get the current time
    const MessageHeader ret_msg_hdr = {
        .command = TIME,
        .payload_size = sizeof(current_time) / sizeof(uint8_t),  // Payload size is 4 bytes (uint32_t)
    };

    // Create the response message
    Message ret_msg = {
        .header = ret_msg_hdr,
        .data = malloc(sizeof(current_time))  // Allocate memory for the payload (uint32_t)
    };

    if (!ret_msg.data) {
        printf("Failed to allocate memory for response payload\n");
        return;
    }

    // Copy the current time into the payload
    uint32_t* tx_data = (uint32_t*)ret_msg.data;
    *tx_data = current_time;  // Set the payload to the current time (uint32_t)

    // Serialize the response message into the tx_buffer
    serialize_message(&ret_msg, tx_buffer);

    // Free the dynamically allocated memory for the response payload
    free(ret_msg.data);
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
	function_map[rx_message.header.command](&rx_message, tx_buffer);
}
