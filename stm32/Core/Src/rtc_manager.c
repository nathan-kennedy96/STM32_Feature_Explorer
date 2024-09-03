/*
 * rtc_manager.c
 *
 *  Created on: Sep 3, 2024
 *      Author: nkenn
 */


#include "rtc_manager.h"
#include <time.h>

RTC_TimeTypeDef currentTime;
RTC_DateTypeDef currentDate;
struct tm currTime;

uint32_t get_rtc_seconds_since_epoch(void) {
    // Get current time and date from RTC
    HAL_RTC_GetTime(&hrtc, &currentTime, RTC_FORMAT_BIN);
    HAL_RTC_GetDate(&hrtc, &currentDate, RTC_FORMAT_BIN);

    // Fill in the tm structure
    currTime.tm_year = currentDate.Year + 100;  // RTC Year is offset from 2000, mktime expects years since 1900
    currTime.tm_mon  = currentDate.Month -1;   // RTC Months are 1-12, tm months are 0-11
    currTime.tm_mday = currentDate.Date;        // Day of the month
    currTime.tm_hour = currentTime.Hours;
    currTime.tm_min  = currentTime.Minutes;
    currTime.tm_sec  = currentTime.Seconds;
    currTime.tm_isdst = -1;                     // Daylight saving time (not used)

    // Convert to seconds since epoch
    time_t timestamp = mktime(&currTime);

    // Return the timestamp as a uint32_t
    return (uint32_t)timestamp;
}

void set_rtc_from_timestamp(uint32_t timestamp) {
    // Convert the timestamp back to a struct tm
    time_t rawtime = (time_t)timestamp;
    struct tm *timeinfo = gmtime(&rawtime);

    // Set the time
    RTC_TimeTypeDef sTime = {0};
    sTime.Hours = timeinfo->tm_hour;
    sTime.Minutes = timeinfo->tm_min;
    sTime.Seconds = timeinfo->tm_sec;
    sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    sTime.StoreOperation = RTC_STOREOPERATION_RESET;
    if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN) != HAL_OK) {
        // Handle error
        Error_Handler();
    }

    // Set the date
    RTC_DateTypeDef sDate = {0};
    sDate.Year = timeinfo->tm_year - 100;  // Year since 2000
    sDate.Month = timeinfo->tm_mon + 1;    // Months are 0-11 in struct tm, 1-12 in RTC
    sDate.Date = timeinfo->tm_mday;
    sDate.WeekDay = timeinfo->tm_wday ? timeinfo->tm_wday : 7;  // Adjust Sunday from 0 to 7
    if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BIN) != HAL_OK) {
        // Handle error
        Error_Handler();
    }
}
