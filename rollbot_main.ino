#include <Servo.h>

#define PIN_THREADMILL        3     // Motor 3 Motor 4 are connected to this pin
#define PIN_DICEVATOR         4     // Motor 1 Motor 2 are connected to this pin
#define PIN_PWM_THREADMILL    5     // Pin that defines the PWM for the Threadmill
#define PIN_PWM_DICEVATOR     6     // Pin that defines the PWM for the Dicevator
#define PIN_SERVO             2     // servo pin
#define PIN_PI_IN             9     // pin connected to PI
#define PIN_PI_OUT            13    // pin connected to PI
#define PIN_THREADMILL_IN     12    // pin connected to PI

#define HOWMANYCHECKS         5     // amount of seconds the storage waits until it decides if the roll failed or not
#define SENSITIVITY           100   // value for the photoresistor
#define TIMEBETWEENDICECHECK  1000  // time in ms between checking if there is a dice present

#define PWM_THREADMILL        255   // PWM of the threadmill
#define PWM_DICEVATOR         255   // PWM of the DICEVATOR

class lopendeBand { // class for the threadmill

  private: bool isThreadmillOn = false;

  public: void init() { // this method initaliazes the pins for the threadmill
      pinMode(PIN_THREADMILL, OUTPUT);
      pinMode(PIN_PWM_THREADMILL, OUTPUT);
      pinMode(PIN_THREADMILL_IN, INPUT);
    }

  public: void doThreadmill() {
      digitalWrite(PIN_THREADMILL, 1); // define the direction of the motor
      analogWrite(PIN_PWM_THREADMILL, PWM_THREADMILL); // define the PWM of the motor
      isThreadmillOn = true;
      Serial.println("Starting Threadmill");
      return "";
    };

  public: void dontThreadmill() {
      digitalWrite(PIN_THREADMILL, 0);
      analogWrite(PIN_PWM_THREADMILL, 0); //PWM of 0 = off
      isThreadmillOn = false;
      Serial.println("Stopping Threadmill");
      return "";
    };

  public: void checkThreadmill() {
      if (digitalRead(PIN_THREADMILL_IN) == HIGH && isThreadmillOn == false) {
        doThreadmill();
      }else
      if (digitalRead(PIN_THREADMILL_IN) == LOW && isThreadmillOn == true) {
        dontThreadmill();
      }
    }
};

class checkerinator { // checkerinator is the class for the photo resistor

  private: int value = 0; // var where the value will be put in

  public: bool checkDice() {
      value = analogRead(PIN_SERVO); //read out photo resistor
      Serial.println((value), DEC); // print for debugging
      if (value > SENSITIVITY) { //check if dice is detected
        return true;
      }
      else {
        return false;
      }
    };
};

class opslag {

    checkerinator diceCounter;
    // init the photoresistor class
    // this is done inside of the storage class because this
    // is the only place where the counter will be used

  private: bool diceIsRolled = true;
  private: bool rollConfirm = false;

  Servo servo;

  public: void init() {
      pinMode(PIN_DICEVATOR, OUTPUT);
      pinMode(PIN_PWM_DICEVATOR, OUTPUT);

      servo.attach(PIN_SERVO);        // initialize servo
      servo.write(50);  // Calibrate servo
      delay(250); // small delay to give the servo time to turn
    };

  public: void openStorage() {
      Serial.println("opening storage"); // print for debugging
      servo.write(170); // open storage
      diceIsRolled = true;
      rollConfirm = false;
      delay(300); // small delay to give the servo time to turn
      Serial.println("closing storage"); // print for debugging
      servo.write(50); // close storage
      delay(300); // small delay to give the servo time to turn
    };

  public: void startDicevator() { //DiceType) {
      digitalWrite(PIN_DICEVATOR, 1); // define the direction of the motor
      analogWrite(PIN_PWM_DICEVATOR, PWM_DICEVATOR); // define the PWM of the motor
    };

  public: void stopDicevator() { //DiceType) {
      digitalWrite(PIN_DICEVATOR, 0);
      analogWrite(PIN_PWM_DICEVATOR, 0); // PWM  of 0 = off
    };

  public: void confirmDice() {

      // this method calls the method of the photoresistor x amount of times.
      // if a dice is detected then it puts the rollConfirm var as true and continues
      // if there's no dice detected after x tries it continues without putting rollConfirm on true

      for (int i = 0; i <= HOWMANYCHECKS; i++) {

        rollConfirm = diceCounter.checkDice();
        if (rollConfirm) {
          break;
        }
        Serial.print("try "); // print for debugging
        Serial.println(i); // print for debugging
        delay(TIMEBETWEENDICECHECK); // this defines the time between checks
      }
      diceIsRolled = false;
    };

  public: bool rollDice() {

      // the rollDice method is the "brain" of the program.
      // first the storage is opened. After it starts the checking
      // if the method returns false then a dice didnt go through and it tries again
      // if it returns true then it worked and continues the program

      while (1) {
        openStorage();
        confirmDice();
        if (rollConfirm == true && diceIsRolled == false) {
          Serial.println("dice detected"); // print for debugging
          return true;
        }
        Serial.println("no dice"); // print for debugging
      }
    };
};

class socket {
  
  lopendeBand threadmill; //initialize the threadmill class

  public: init() {
      pinMode(PIN_PI_IN, INPUT);
      pinMode(PIN_PI_OUT, OUTPUT);
      threadmill.init();
    }

  public: void waitForPi() {
      while (1) {
        if (digitalRead(PIN_PI_IN)) {
          break;
        }
        Serial.println("waiting"); // print for debugging
        threadmill.checkThreadmill();
        delay(500);
      }
    }

  public: void sendToPi() {
      digitalWrite(PIN_PI_OUT, HIGH);
      delay(500);
      digitalWrite(PIN_PI_OUT, LOW);
    }

};

//start main code

opslag storage; //initialize the storage class
socket sock;

void setup() {
  Serial.begin(9600);

  storage.init();
  sock.init();
}

void loop() {

  //  threadmill.doThreadmill();
  //  delay(1000);
  //  threadmill.stopThreadmill();
  //  delay(1000);

  sock.waitForPi();
  Serial.println("starting"); // print for debugging
  storage.rollDice();
  Serial.println("Dicevator started"); // print for debugging
  storage.startDicevator();
  delay(5000);
  storage.stopDicevator();
  Serial.println("Dicevator stopped"); // print for debugging
  Serial.println("done"); // print for debugging
  sock.sendToPi();


}
