/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

  /* Includes ------------------------------------------------------------------*/
#include "modulator.h"

void send_byte(Mod_Info *modulator, uint8_t byte){
	modulator->data_byte = byte;
}
