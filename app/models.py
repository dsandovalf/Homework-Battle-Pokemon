from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import current_user

followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on  = db.Column(db.DateTime, default=dt.utcnow)
    pokemons = db.relationship('Pokemon', backref='trainer', lazy='dynamic') #???
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    followed = db.relationship('User',
                    secondary = followers,
                    primaryjoin=(followers.c.follower_id == id),
                    secondaryjoin=(followers.c.followed_id == id),
                    backref=db.backref('followers',lazy='dynamic'),
                    lazy='dynamic'
                    )
    # We want to check if the user is following someone
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # def has_pokemon(self, pokemon):
    #     if Pokemon.query.:
    #         return True
    #     else:
    #         return False 

    # follow a user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    # unfollow a user
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    # get all the posts from the users I am following
    def followed_posts(self):
        #get posts for all the users I'm following
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
        #get all my own posts
        self_posts = Post.query.filter_by(user_id=self.id)

        #add those together and then I want to sort then my dates in descending order
        all_posts = followed.union(self_posts).order_by(Post.date_created.desc())
        return all_posts

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.icon = data['icon']
        self.password = self.hash_password(data['password'])

    def hash_password(self, original_password): #50 minutes interview question 
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_icon_url(self):
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{self.icon}.gif'

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    # SELECT * FROM user WHERE id = ???


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # saves the Post to the database
    def save(self):
        db.session.add(self) # add the Post to the db session
        db.session.commit() #save everything in the session to the database

    def edit(self, new_body):
        self.body=new_body
        self.save()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<id:{self.id} | Post: {self.body[:15]}>'

        
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name =db.Column(db.String(100), unique=True, index=True)
    ability = db.Column(db.String(100))
    base_experience = db.Column(db.Integer)
    base_hp = db.Column(db.Integer)
    base_defense = db.Column(db.Integer)
    base_attack = db.Column(db.Integer)
    front_shiny = db.Column(db.String(600))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def battle(self, poke_points):
        total_points =  Pokemon.base_hp + Pokemon.base_attack + Pokemon.base_defense
        if total_points > poke_points:
            return "You won!"
        if  Pokemon.base_attack > Pokemon.base_defense:
            total_points += (Pokemon.base_attack - Pokemon.base_defense)
        else:
            return "You lost points" 
            

    # def limit_pokebag(self, pokemon):
    #     return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def from_dict(self, data):
        self.pokemon_name = data['name']
        self.ability = data['ability']
        self.base_experience = data["base_experience"]
        self.base_hp = data['base_hp']
        self.base_defense = data['base_defense']
        self.base_attack = data['base_attack']
        self.front_shiny = data['front_shiny']
        self.user_id = current_user.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, new_pokemon_name, new_ability, new_base_experience, new_base_hp, new_base_defense, new_base_attack, new_front_shiny):
        self.pokemon_name = new_pokemon_name
        self.ability = new_ability
        self.base_experience = new_base_experience
        self.base_hp = new_base_hp
        self.base_defense = new_base_defense
        self.base_attack = new_base_attack
        self.front_shiny = new_front_shiny
        self.save()

    def __repr__(self):
        return f'<id: {self.id} | Pokemon: {self.pokemon_name}>'
    