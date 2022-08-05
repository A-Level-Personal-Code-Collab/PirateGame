from rest_framework.serializers import ModelSerializer, ValidationError

from master.models import Player

class PlayerSerializer(ModelSerializer):
    
    #! Current system entrusts clients to validate nickname. Server validation is disabled.
    def DISABLED_validate_player_nickname(self,nickname):
        NICKNAME_MAX_LEN = 15
        NICKNAME_MIN_LEN = 3
        BLACKLIST_FILE = "player/static/nickname-word-blacklist.csv"

        nickname = nickname.lower().replace(" ","")

        #---------------#
        #Simple length check (seconds javascript check)
        self.nicknameLen = len(nickname)
        if self.nicknameLen > NICKNAME_MAX_LEN or self.nicknameLen < NICKNAME_MIN_LEN:
            raise ValidationError("Nickname Rejected: Incorrect length")
        
        #---------------#
        #Checks banned words lists
        self.blacklist = open(BLACKLIST_FILE, 'r')
        self.rejectWords = self.blacklist.read().split(",")
        self.blacklist.close()

        #Loop through banned words and check them all
        for word in self.rejectWords:
            wordLen = len(word)
            if not wordLen > self.nicknameLen: #If word in question is longer than nickname then ignore it
                if word == nickname: #Check if word _is_ nickname
                    raise ValidationError("Nickname rejected: Profanity")
                numSubstrings = self.nicknameLen - wordLen + 1 #Calculated how many possible substrings there are of any given word
                for i in range(numSubstrings): #Finds and checks all substrings of nickname to the length of the check word
                    substring = nickname[i:i+wordLen]
                    if substring == word:
                        raise ValidationError("Nickname Rejected: Contains profanity")

        return nickname

    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ['player_id']  # This is generated automatically on save