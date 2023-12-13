/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MODULATOR_H
#define __MODULATOR_H

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include "circular_buffer.h"


/**
  * @brief  TIM Slave configuration Structure definition
  */
typedef struct {
	uint8_t data_byte;
	uint8_t periods_between_bytes;
    uint8_t available;
} Mod_Info;


void init();

// void send_byte(Mod_Info *modulator, uint8_t byte);

void tx_byte(uint8_t byte);

void check_tx_buffer(Mod_Info *modulator);

#ifdef __cplusplus
}
#endif

#endif /* __MODULATOR_H */