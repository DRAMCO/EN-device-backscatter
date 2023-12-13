/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

  /* Includes ------------------------------------------------------------------*/
#include "modulator.h"

uint8_t transmit_buffer [10];
CircularBuffer tx_buffer_manager;

void init(){
    init_buffer(&tx_buffer_manager, transmit_buffer, sizeof(transmit_buffer));
}

// void send_byte(Mod_Info *modulator, uint8_t byte){
// 	modulator->data_byte = byte;
//     modulator->send_byte_now = 1;
// }

void tx_byte(uint8_t byte){
    push(&tx_buffer_manager, byte);
}

void check_tx_buffer(Mod_Info *modulator){
    if(!is_empty(&tx_buffer_manager)){
        modulator->data_byte = pull(&tx_buffer_manager);
        modulator->available = 1;
    }
}