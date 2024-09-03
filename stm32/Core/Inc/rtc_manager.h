/*
 * rtc_manager.h
 *
 *  Created on: Sep 3, 2024
 *      Author: nkenn
 */

#ifndef INC_RTC_MANAGER_H_
#define INC_RTC_MANAGER_H_

#include "stm32f4xx_hal.h"

// Declare the RTC handle as extern
extern RTC_HandleTypeDef hrtc;

// Function to get time from RTC in seconds since epoch
uint32_t get_rtc_seconds_since_epoch(void);
void set_rtc_from_timestamp(uint32_t);

#endif /* INC_RTC_MANAGER_H_ */
