import pandas as pd 

df = pd.read_csv('./spotify_dataset.csv')
def main():
    display_analyzer()
    analyzer.display_top_users()
class SpotifyUser:
    def __init__(self, user_id, gender, age, country, subscription_type, listening_time, songs_played_per_day, skip_rate, device_type, ads_listened_per_week, offline_listening, is_churned):
        self.user_id = user_id
        self.gender = gender
        self.age = age
        self.country = country
        self.subscription_type = subscription_type
        self.listening_time = listening_time
        self.songs_played_per_day = songs_played_per_day
        self.skip_rate = skip_rate
        self.device_type = device_type
        self.ads_listened_per_week = ads_listened_per_week
        self.offline_listening = offline_listening
        self.is_churned = is_churned
    def is_free_user(self):
        return self.subscription_type == "Free"
    def has_churned(self):
        return self.is_churned == 1
    def is_super_fan(self):
        return self.songs_played_per_day >= 60
    def is_casual_listener(self):
        return self.songs_played_per_day < 20
    def is_ad_overloaded(self):
        return self.subscription_type == 'Free' and self.ads_listened_per_week >= 25
    def is_at_risk(self):
        return self.subscription_type == 'Free' and self.ads_listened_per_week > 20 and self.skip_rate > 0.35
    def is_good_premium_candidate(self):
        return self.subscription_type == 'Free' and self.songs_played_per_day >= 40 and self.ads_listened_per_week >= 15 and self.is_churned == 0
    def get_profile_label(self):
        if self.is_super_fan():
            return "Fan absolu"
        elif self.is_good_premium_candidate():
            return "Candidat Premium"
        elif self.is_at_risk():
            return "À risque"
        elif self.is_ad_overloaded():
            return 'Noyé sous les pubs'
        elif self.is_casual_listener():
            return "Auditeur tranquille"
        else:
            return "Utilisateur standard"
class SpotifyAnalyzer:
    def __init__(self, filepath):
        self.users = []
        df = pd.read_csv(filepath)
        for index, row in df.iterrows():
            user = SpotifyUser(
                row['user_id'],
                row['gender'],
                row['age'],
                row['country'],
                row['subscription_type'], 
                row['listening_time'], 
                row['songs_played_per_day'], 
                row['skip_rate'], 
                row['device_type'], 
                row['ads_listened_per_week'], 
                row['offline_listening'], 
                row['is_churned']
            )
            self.users.append(user)
    def count_users(self):
        return len(self.users)
    def average_age(self):
        ages = [user.age for user in self.users]
        return sum(ages) / len(ages)
    def average_listening_time(self):
        listening_time = [user.listening_time for user in self.users]
        return sum(listening_time)/len(listening_time)
    def average_songs_played_per_day(self):
        songs_played_per_day = [user.songs_played_per_day for user in self.users]
        return sum(songs_played_per_day)/len(songs_played_per_day)
    def rate_churn(self):
        churn = [user for user in self.users if user.has_churned()]
        return (len(churn) / len(self.users)) * 100
    def sub_max(self):
        sub = [user.subscription_type for user in self.users]
        return max(sub, key=sub.count)
    def device_max(self):
        device = [user.device_type for user in self.users]
        return max(device, key=device.count)
    def count_super_fan(self):
        fans = [user for user in self.users if user.is_super_fan()]
        return len(fans)
    def count_casual_listener(self):
        casuals = [user for user in self.users if user.is_casual_listener()]
        return len(casuals)
    def count_overloaded_user(self):
        overloaded = [user for user in self.users if user.is_ad_overloaded()]
        return len(overloaded)
    def count_user_at_risk(self):
        risk = [user for user in self.users if user.is_at_risk()]
        return len(risk)
    def count_premium_user(self):
        premium = [user for user in self.users if user.subscription_type == "Premium"]
        return len(premium)
    def display_top_users(self):
        print("=== Top 5 des plus gros auditeurs ===")
        top5 = sorted(self.users, key=lambda user: user.songs_played_per_day, reverse=True)[:5] 
        for user in top5:
            print(f"{user.user_id} - {user.age} ans - {user.country}")
            print(f'{user.subscription_type} || {user.songs_played_per_day} songs per day || {user.get_profile_label()}')
        print("=== Top 5 des utilisateurs à risque ===")
        at_risk = [user for user in self.users if user.is_at_risk()]
        for user in at_risk[:5]:
            print(f"{user.user_id} - {user.age} ans - {user.country}")
            print(f'{user.ads_listened_per_week} || {user.skip_rate} || {user.songs_played_per_day} songs per day || {user.get_profile_label()}')

analyzer = SpotifyAnalyzer('./spotify_dataset.csv')



def display_analyzer():
    print('=== Spotify Talent Scout ===')
    print(f'Nombre total d\'utilisateurs : {analyzer.count_users()}')
    print(f'Âge moyen : {analyzer.average_age():.2f} ans')
    print(f'Temps d\'écoute moyen : {analyzer.average_listening_time():.2f} minutes')
    print(f'Chansons jouées par jour en moyenne : {analyzer.average_songs_played_per_day():.2f} ')
    print(f'Taux de churn : {analyzer.rate_churn():.2f} %')
    print(f'Abonnement le plus représenté : {analyzer.sub_max()}')
    print(f'Appareil le plus utilisé : {analyzer.device_max()}')
    print(f'Fans absolus : {analyzer.count_super_fan()}')
    print(f'Auditeurs tranquilles : {analyzer.count_casual_listener()}')
    print(f'Utilisateurs noyés sous les pubs : {analyzer.count_overloaded_user()}')
    print(f'Utilisateurs à risque : {analyzer.count_user_at_risk()}')
    print(f'Candidats Premium : {analyzer.count_premium_user()}')
    print('=== Spotify Talent Scout ===')
    
if __name__ == "__main__":
    main()

