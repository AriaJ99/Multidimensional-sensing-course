int sensorPin[4] = {A0,A1,A2,A3}; // select the input pin for LDR

int sensorValue = 0; // variable to store the value coming from the sensor
long int Avg(long int arr[],int size){
	
  long int sum=0;
  for(int i=0;i<size;i++){
    sum+=arr[i];
  }
  return sum/size;
}
long int Avg(int arr[],int size){
	
  long int sum=0;
  for(int i=0;i<size;i++){
    sum+=arr[i];
  }
  return sum/size;
}
long int Variance(int arr[],long int mean,int size){
  long int sum=0;
  for(int i=0;i<size;i++)
  	sum+=(arr[i]-mean)*(arr[i]-mean);
  
  return sum/(size-1);
}
long int Variance(long int arr[],long int mean,int size){
  long int sum=0;
  for(int i=0;i<size;i++)
  	sum+=(arr[i]-mean)*(arr[i]-mean);
  
  return sum/(size-1);
}
int fault_detector(long int mean[],long int variance[]){
//detects a faulty sensor(assuming there's only one faulty sensor)
//this function checks two variance and mean to find the faulty sensor
//one scenario is if average mean value difference is higher than a threshold 
//the other scenario is when vaiance is higher or less than a coefficient of the average threshold
  int threshold=300;
  int coeff=10;
  long int ovr_mean,ovr_variance;
  ovr_mean=Avg(mean,4);
  ovr_variance=Avg(variance,4);
  for(int i=0;i<4;i++){
  	if(mean[i]>ovr_mean+threshold || mean[i]<ovr_mean-threshold)
      return i;
    if(variance[i]>ovr_variance*coeff || variance[i]<ovr_variance/coeff)
      return i;
  }
  //no faulty sensor found 
  return -1;
}
void setup() {
Serial.begin(9600); //sets serial port for communication
}
void loop() {
  Serial.println("loop");
  long int value[4];
  int buffer[4][101];
  int buffer_pointer[4]={0,0,0,0};
  for(int i=0;i<4;i++){
	sensorValue = analogRead(sensorPin[i]); // read the value from the sensor
    Serial.println(sensorValue); //prints the values coming from the sensor on the screen
	value[i]=sensorValue;
    int ptr=buffer_pointer[i]++%100;
    buffer[i][ptr]=sensorValue;  
  }
  int mean1=Avg(value,4);
  long int variance1=Variance(value,mean1,4);
  //print average and variance for the current input
  Serial.print("Average : ");
  Serial.println(mean1);
  Serial.print("Variance : ");
  Serial.println(variance1);
  //print average and variance for each sensor over a 100 recent inputs
  long int mean[4],variance[4];
  for(int i=0;i<4;i++){
   int cnt=0;
   if(buffer_pointer[i]>99)
     cnt=100;
   else
     cnt=buffer_pointer[i]+1;
   mean[i]=Avg(buffer[i],cnt);
   variance[i]=Variance(buffer[i],mean[i],cnt);
   Serial.print("Average for sensor ");
   Serial.print(i+1);
   Serial.print(" : ");
   Serial.print(mean[i]);
   Serial.println();
   Serial.print("Variance for sensor ");
   Serial.print(i+1);
   Serial.print(" : ");
   Serial.print(variance[i]);
   Serial.println();
    
   }
  // faulty sensor detection
  int faulty_sensor=fault_detector(mean,variance);
  if(faulty_sensor>=0){
   Serial.print("Sensor number ");
   Serial.print(faulty_sensor+1);
   Serial.println(" is faulty");
  }
delay(2000);
  
  }