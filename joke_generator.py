"""Joke Generator - Using External API"""
import requests
import json
from typing import Dict, List, Optional

class JokeGenerator:
    """Generate random jokes using external APIs"""
    
    def __init__(self):
        # Multiple joke APIs for fallback
        self.apis = {
            'official_joke_api': 'https://official-joke-api.appspot.com',
            'jokes_ninja': 'https://api.api-ninjas.com/v1/jokes',
            'random_joke': 'https://random-joke-api.herokuapp.com/random'
        }
        self.current_api = 'official_joke_api'

    def get_random_joke(self) -> Optional[Dict]:
        """Get a random joke from Official Joke API"""
        try:
            url = f"{self.apis['official_joke_api']}/random_joke"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            joke_data = response.json()
            return {
                'setup': joke_data.get('setup', ''),
                'punchline': joke_data.get('punchline', ''),
                'type': joke_data.get('type', 'general'),
                'api': 'Official Joke API',
                'full_joke': f"{joke_data.get('setup', '')} {joke_data.get('punchline', '')}"
            }
        except Exception as e:
            print(f"Error fetching from Official Joke API: {e}")
            return self.get_joke_fallback()

    def get_joke_by_type(self, joke_type: str = 'general') -> Optional[Dict]:
        """Get a joke by specific type"""
        valid_types = ['general', 'programming', 'knock-knock']
        
        if joke_type not in valid_types:
            joke_type = 'general'
        
        try:
            url = f"{self.apis['official_joke_api']}/jokes/{joke_type}/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            joke_data = response.json()
            if isinstance(joke_data, list):
                joke_data = joke_data[0]
            
            return {
                'setup': joke_data.get('setup', ''),
                'punchline': joke_data.get('punchline', ''),
                'type': joke_data.get('type', joke_type),
                'api': 'Official Joke API',
                'full_joke': f"{joke_data.get('setup', '')} {joke_data.get('punchline', '')}"
            }
        except Exception as e:
            print(f"Error fetching {joke_type} joke: {e}")
            return self.get_random_joke()

    def get_programming_joke(self) -> Optional[Dict]:
        """Get a programming joke"""
        return self.get_joke_by_type('programming')

    def get_knockknock_joke(self) -> Optional[Dict]:
        """Get a knock-knock joke"""
        return self.get_joke_by_type('knock-knock')

    def get_multiple_jokes(self, count: int = 5) -> List[Dict]:
        """Get multiple random jokes"""
        jokes = []
        for _ in range(count):
            joke = self.get_random_joke()
            if joke:
                jokes.append(joke)
        return jokes

    def get_joke_fallback(self) -> Optional[Dict]:
        """Fallback: Use local jokes if API fails"""
        local_jokes = [
            {
                'setup': "Why don't scientists trust atoms?",
                'punchline': "Because they make up everything!",
                'type': 'general',
                'api': 'Local Fallback',
                'full_joke': "Why don't scientists trust atoms? Because they make up everything!"
            },
            {
                'setup': "What do you call a fake noodle?",
                'punchline': "An impasta!",
                'type': 'general',
                'api': 'Local Fallback',
                'full_joke': "What do you call a fake noodle? An impasta!"
            },
            {
                'setup': "Why did the scarecrow win an award?",
                'punchline': "He was outstanding in his field!",
                'type': 'general',
                'api': 'Local Fallback',
                'full_joke': "Why did the scarecrow win an award? He was outstanding in his field!"
            }
        ]
        import random
        return random.choice(local_jokes)

    def format_joke(self, joke: Dict) -> str:
        """Format joke for display"""
        if not joke:
            return "Could not generate joke"
        
        output = f"\n{'='*50}\n"
        output += f"📝 {joke['full_joke']}\n"
        output += f"Type: {joke['type']}\n"
        output += f"Source: {joke['api']}\n"
        output += f"{'='*50}\n"
        return output


class AdvancedJokeGenerator(JokeGenerator):
    """Extended joke generator with more features"""
    
    def __init__(self):
        super().__init__()
        self.joke_history = []
        self.favorites = []

    def add_to_favorites(self, joke: Dict):
        """Add joke to favorites"""
        self.favorites.append(joke)

    def get_favorites(self) -> List[Dict]:
        """Get all favorite jokes"""
        return self.favorites

    def get_joke_history(self) -> List[Dict]:
        """Get joke generation history"""
        return self.joke_history

    def generate_with_history(self) -> Optional[Dict]:
        """Generate joke and add to history"""
        joke = self.get_random_joke()
        if joke:
            self.joke_history.append(joke)
        return joke

    def search_jokes_by_keyword(self, keyword: str) -> List[Dict]:
        """Search through history for jokes containing keyword"""
        results = []
        for joke in self.joke_history:
            if keyword.lower() in joke['full_joke'].lower():
                results.append(joke)
        return results

    def export_jokes(self, filename: str = 'jokes.json'):
        """Export jokes to JSON file"""
        data = {
            'history': self.joke_history,
            'favorites': self.favorites
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Jokes exported to {filename}")

    def import_jokes(self, filename: str = 'jokes.json'):
        """Import jokes from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.joke_history = data.get('history', [])
            self.favorites = data.get('favorites', [])
            print(f"Jokes imported from {filename}")
        except Exception as e:
            print(f"Error importing jokes: {e}")


def main():
    """Main demonstration"""
    print("\n🎉 Welcome to Joke Generator! 🎉\n")
    
    # Initialize generator
    generator = AdvancedJokeGenerator()
    
    # Get random joke
    print("📍 Random Joke:")
    joke = generator.get_random_joke()
    print(generator.format_joke(joke))
    generator.add_to_favorites(joke)
    
    # Get programming joke
    print("📍 Programming Joke:")
    prog_joke = generator.get_programming_joke()
    print(generator.format_joke(prog_joke))
    
    # Get knock-knock joke
    print("📍 Knock-Knock Joke:")
    kk_joke = generator.get_knockknock_joke()
    print(generator.format_joke(kk_joke))
    
    # Get multiple jokes
    print("📍 Multiple Jokes (3):")
    multiple = generator.get_multiple_jokes(3)
    for i, j in enumerate(multiple, 1):
        print(f"\nJoke {i}:")
        print(generator.format_joke(j))
    
    # Show favorites
    print(f"\n❤️ Favorite Jokes: {len(generator.get_favorites())}")
    for fav in generator.get_favorites():
        print(f"  - {fav['full_joke'][:60]}...")


if __name__ == "__main__":
    main()
