/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

  /* Includes ------------------------------------------------------------------*/
#include "modulator.h"

void tx_send(bc_handler_struct *bc, const uint8_t *buffer, uint16_t lenght){
    
    //  Reset counters
    bc->current_byte = 0;
    bc->current_bit = 7;

    //  Share pointer and length
    bc->buffer = buffer;
    bc->num_bytes = lenght;

    //  Change status to 'SENDING'
    bc->status = SENDING;
}
