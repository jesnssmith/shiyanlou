import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    user_data = {} #dict with shape{'user_id':{'score':, 'submit_time':}}
    user=[]        # list with shape [(user_id, score, submit_time)]
    user_ids=set() #contain all user_id
    for contest in contests.find():
        user_ids.add(contest.get('user_id'))
        if user_data.get(contest.get('user_id')):
            user_data[contest.get('user_id')]['score'] += contest.get('score')
            user_data[contest.get('user_id')]['submit_time'] += contest.get('submit_time')
        else:
            user_data[contest.get('user_id')]={'score' : contest.get('score'), 'submit_time' : contest.get('submit_time')}

    for i,j in user_data.items():
        user.append((i,j['score'],j['submit_time']))
    sort_user = sorted(user,key=lambda x:(-x[1] ,x[2]))  # sorted user

    # use index of sort_user to get rank
    for i,j in enumerate(sort_user):
        user_data[j[0]]['rank'] = i + 1

    if user_id not in user_ids:
        return "Parameter Error"
    # return sort_user
    return user_data[int(user_id)]['rank'], user_data[int(user_id)]['score'], user_data[int(user_id)]['submit_time']
if __name__ == '__main__':
    
    if len(sys.argv[1:]) > 1:
        print("Parameter Error")
    else:
        try:

            user_id = int(sys.argv[1])
            userdata = get_rank(user_id)
            print(userdata)
        except:
            print("Parameter Error")

