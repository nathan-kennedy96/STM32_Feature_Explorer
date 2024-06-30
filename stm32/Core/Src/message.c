/*
 * message.c
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */


#include "message.h"

void deserialize_message(const uint8_t* buffer, Message* msg) {
	memcpy((uint8_t*)msg, buffer, sizeof(Message));
}
void serialize_message(const Message* msg, uint8_t* buffer) {
	 memcpy(buffer, (uint8_t*)msg, sizeof(Message));
}
