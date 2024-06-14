#include <UniversalTelegramBot.h>
#include <WiFiClientSecure.h>
#include <WiFi.h>
char *ssid = "Tartarous";
char *password = "ajhv6004";
#define BOTtoken "7340670419:AAG4OWLNV2uXI5h2HxlQK2zSpFrlm4le1d4"

WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

int bot_mtbs = 1000; // min time between scan message
long bot_lastTime; // last time messages' scan has been done
bool start = false;
int ledPin = 4;
int ledStatus = 0;

void handleNewMessages(int numNewMessages){
  Serial.println("handle New Messages");
  Serial.println(String(numNewMessages));

  for(int i = 0; i < numNewMessages; ++i){
    String chat_id = String(bot.messages[i].chat_id);
    String text = bot.messages[i].text;
    Serial.print(chat_id);

    String from_name = bot.messages[i].from_name;
    if(from_name == "") from_name = "Guest";
    if (text == "/ledon") {
      digitalWrite(ledPin, HIGH);
      ledStatus = 1;
      bot.sendMessage(chat_id, "LED is ON", "");
    }
    if (text == "/ledoff") {
      digitalWrite(ledPin, LOW);
      ledStatus = 0;
      bot.sendMessage(chat_id, "LED is OFF", "");
    }
    if (text == "/status") {
      if(ledStatus)
        bot.sendMessage(chat_id, "LED is ON", "");
      else 
        bot.sendMessage(chat_id, "LED is OFF", "");
    }
    if(text == "/options"){
      String keyboardJson = "[[\"/ledon\", \"/ledoff\"], [\"/status\"]]";
      bot.sendMessageWithReplyKeyboard(chat_id, "Choose from one of the following options", "", keyboardJson, true);
    }
    if (text == "/start") {
      Serial.println("***");
      String welcome = "Welcome to Karimi Bot, "+from_name+".\n";
      welcome += "This is Flash Led Bot.\n\n";
      welcome += "/ledon : to switch the Led ON\n";
      welcome += "/ledoff : to switch the Led OFF\n";
      welcome += "/status : returns current status of LED\n";
      welcome += "/options : returns the reply keyboard\n";
      bot.sendMessage(chat_id, welcome, "Markdown");
    }
  }
}

void setup(){
  Serial.begin(115200);
  Serial.print("Connecting WiFi:");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  pinMode(ledPin, OUTPUT);
  delay(10);
  digitalWrite(ledPin, LOW);
}
void loop(){
  if(millis() > bot_lastTime + bot_mtbs){
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while(numNewMessages){
      Serial.println("got response");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    bot_lastTime = millis();
  }
}