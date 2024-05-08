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
typedef enum {
    SENDING,
    IDLE,
} bc_handler_status;

typedef struct {
  bc_handler_status status;
	uint8_t *buffer;
  uint8_t num_bytes;
  uint8_t current_byte;
  uint8_t current_bit;
} bc_handler_struct;


void tx_send(bc_handler_struct *bc, uint8_t *buffer, uint8_t lenght);

#ifdef __cplusplus
}
#endif

#endif /* __MODULATOR_H */