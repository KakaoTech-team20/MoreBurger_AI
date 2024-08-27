import app.rds_dataloader.burger as burger
import app.rds_dataloader.user as user

# 연결
print(burger.get_burger_by_id(1))
print(user.get_user_by_id(1))


