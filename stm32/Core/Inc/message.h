/*
 * message.h
 *
 *  Created on: Jun 28, 2024
 *      Author: nkenn
 */

#ifndef INC_MESSAGE_H_
#define INC_MESSAGE_H_

#include "command.h"
#include <stdint.h>   // Include standard integer types

typedef struct {
    uint8_t command;
    uint8_t payload_size;
} MessageHeader;

typedef struct {
    MessageHeader header;
    void* data;
} Message;

void deserialize_message(const uint8_t* buffer, Message* msg);
void serialize_message(const Message* msg, uint8_t* buffer);

#endif /* INC_MESSAGE_H_ */
