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


/**
  * @brief  TIM Slave configuration Structure definition
  */
typedef struct
{
	uint8_t data_byte;
	uint8_t periods_between_bytes;

} Mod_Info;


void send_byte(Mod_Info *modulator, uint8_t byte);

#ifdef __cplusplus
}
#endif

#endif /* __MODULATOR_H */

