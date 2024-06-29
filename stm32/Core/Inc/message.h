/*
 * message.h
 *
 *  Created on: Jun 28, 2024
 *      Author: nkenn
 */

#ifndef INC_MESSAGE_H_
#define INC_MESSAGE_H_

#include "command.h"

typedef struct {
    Command cmd;
    uint16_t data;
} Message;

#endif /* INC_MESSAGE_H_ */
