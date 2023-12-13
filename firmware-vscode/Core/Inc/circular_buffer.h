/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __CIRCULAR_BUFFER_H
#define __CIRCULAR_BUFFER_H

#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>


typedef struct {
    uint8_t* buffer;
    uint8_t size;
    uint8_t head; // Index where the next element will be pushed
    uint8_t tail; // Index where the next element will be pulled
} CircularBuffer;


// // Define the circular buffer structure
// struct CircularBuffer {
//     uint8_t* buffer;
//     uint8_t size;
//     uint8_t head; // Index where the next element will be pushed
//     uint8_t tail; // Index where the next element will be pulled
// };


void init_buffer(CircularBuffer* cb, uint8_t* buffer, uint8_t size);
void push(CircularBuffer* cb, uint8_t value);
uint8_t pull(CircularBuffer* cb);
uint8_t is_empty(CircularBuffer* cb);

#ifdef __cplusplus
}
#endif

#endif /* __MODULATOR_H */