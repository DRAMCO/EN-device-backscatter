/**
  ******************************************************************************
  * @file    modulator.h
  * @author  Jarne Van Mulders
  * @brief   
  ******************************************************************************
  */

  /* Includes ------------------------------------------------------------------*/

#include "circular_buffer.h"

// Function to initialize the circular buffer
void init_buffer(CircularBuffer* cb, uint8_t* buffer, uint8_t size) {
    cb->buffer = buffer;
    cb->size = size;
    cb->head = 0;
    cb->tail = 0;
}

// Function to push an element into the buffer
void push(CircularBuffer* cb, uint8_t value) {
    cb->buffer[cb->head] = value;
    cb->head = (cb->head + 1) % cb->size;
}

// Function to pull an element from the buffer
uint8_t pull(CircularBuffer* cb) {
    uint8_t value = cb->buffer[cb->tail];
    cb->tail = (cb->tail + 1) % cb->size;
    return value;
}

// Function to check if the buffer is empty
uint8_t is_empty(CircularBuffer* cb) {
    return cb->head == cb->tail;
}
