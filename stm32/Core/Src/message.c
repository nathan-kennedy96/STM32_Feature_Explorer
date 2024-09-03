/*
 * message.c
 *
 *  Created on: Jun 30, 2024
 *      Author: nkenn
 */


#include "message.h"

void serialize_message(const Message* msg, uint8_t* buffer) {
    // Serialize Command (2 bytes, little-endian)
    buffer[0] = msg->cmd & 0xFF;          // LSB first
    buffer[1] = (msg->cmd >> 8) & 0xFF;   // MSB next

    // Serialize uint32_t data (4 bytes, little-endian)
    buffer[2] = msg->data & 0xFF;             // LSB first
    buffer[3] = (msg->data >> 8) & 0xFF;
    buffer[4] = (msg->data >> 16) & 0xFF;
    buffer[5] = (msg->data >> 24) & 0xFF;     // MSB last

}

void deserialize_message(const uint8_t* buffer, Message* msg) {
    // Deserialize Command (2 bytes, little-endian)
    msg->cmd = (Command)(buffer[0] | (buffer[1] << 8));

    // Deserialize uint32_t data (4 bytes, little-endian)
    msg->data = (uint32_t)(buffer[2] | (buffer[3] << 8) | (buffer[4] << 16) | (buffer[5] << 24));
}

