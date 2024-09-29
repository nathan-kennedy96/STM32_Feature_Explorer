/*
 * message.c
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */


#include "message.h"
#include <stdlib.h>
#include <stddef.h>

void serialize_message(const Message* msg, uint8_t* buffer) {
    // Serialize Command
    buffer[0] = (uint8_t)msg->header.command;
    // Serialize the payload size
    buffer[1] = msg->header.payload_size;

    //To serialize the payload we must know the type:
    int type_code = Command_type_map[msg->header.command];
    
    // The index starts at 2
    size_t index = 2;
     // Serialize the payload based on its type
    switch (type_code) {
        case 0: { // uint8_t payload
            uint8_t* data = (uint8_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                buffer[index++] = data[i];
            }
            break;
        }
        case 1: { // uint16_t payload
            uint16_t* data = (uint16_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                buffer[index++] = data[i] & 0xFF;           // LSB
                buffer[index++] = (data[i] >> 8) & 0xFF;    // MSB
            }
            break;
        }
        case 2: { // uint32_t payload
            uint32_t* data = (uint32_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                buffer[index++] = data[i] & 0xFF;           // LSB
                buffer[index++] = (data[i] >> 8) & 0xFF;
                buffer[index++] = (data[i] >> 16) & 0xFF;
                buffer[index++] = (data[i] >> 24) & 0xFF;   // MSB
            }
            break;
        }

    }
}

// Function to deserialize a message from a byte buffer
void deserialize_message(const uint8_t* buffer, Message* msg) {
    // Deserialize Command (1 byte)
    msg->header.command = buffer[0];

    // Deserialize Payload Size (1 byte)
    msg->header.payload_size = buffer[1];

    // Determine the type of the payload based on the command
    int type_code = Command_type_map[msg->header.command];

    // Allocate memory for the payload based on the payload size and type
    switch (type_code) {
        case 0: { // uint8_t payload
            msg->data = malloc(msg->header.payload_size * sizeof(uint8_t));
            uint8_t* data = (uint8_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                data[i] = buffer[2 + i];  // Deserialize each byte
            }
            break;
        }
        case 1: { // uint16_t payload
            msg->data = malloc(msg->header.payload_size * sizeof(uint16_t));
            uint16_t* data = (uint16_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                data[i] = buffer[2 + i * 2] | (buffer[2 + i * 2 + 1] << 8);  // Deserialize each uint16_t
            }
            break;
        }
        case 2: { // uint32_t payload
            msg->data = malloc(msg->header.payload_size * sizeof(uint32_t));
            uint32_t* data = (uint32_t*)msg->data;
            for (size_t i = 0; i < msg->header.payload_size; i++) {
                data[i] = buffer[2 + i * 4] |
                          (buffer[2 + i * 4 + 1] << 8) |
                          (buffer[2 + i * 4 + 2] << 16) |
                          (buffer[2 + i * 4 + 3] << 24);  // Deserialize each uint32_t
            }
            break;
        }
    }
}

