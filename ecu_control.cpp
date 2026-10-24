#include <iostream>
 
// MISRA Violation: Using raw pointer without boundaries
// ISO 26262 Concern: No validation of input values

void processSensorData(int* rawData) {
   // Dangerous: potential null-pointer dereference
   int value = *rawData;

   // MISRA Violation: Dynamic memory allocation (malloc/new is banned in ASIL systems)
   int* calculatedValue = new int(value * 2);

   std::cout << "Sensor output: " << *calculatedValue << std::endl;

   // Potential Memory Leak if deleted improperly
   delete calculatedValue;
}

