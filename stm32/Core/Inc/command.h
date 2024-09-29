/*
 * command.h
 *
 *  Created on: Jun 28, 2024
 *      Author: nkenn
 */

#ifndef INC_COMMAND_H_
#define INC_COMMAND_H_

typedef enum {
    NOK = 0,
    HELLO = 1,
	TIME = 2,
} Command;

// 0 - uint8_t
// 1 - uint16_t
// 2 - uint32_t

extern int Command_type_map[];

#endif /* INC_COMMAND_H_ */
