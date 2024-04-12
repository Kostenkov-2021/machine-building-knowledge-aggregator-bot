@router.message(commands=['subscribe'])
async def subscribe(message: types.Message):
    args = message.get_args().split()
    if args[0] == "tag":
        tag_id = int(args[1])
        subscribe_to_tag(get_db(), message.from_user.id, tag_id)
        await message.answer("Вы подписались на тег.")
    elif args[0] == "responses":
        subscribe_to_responses(get_db(), message.from_user.id)
        await message.answer("Вы подписались на уведомления о ответах.")

@router.message(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    subscription_id = int(message.get_args())
    unsubscribe(get_db(), message.from_user.id, subscription_id)
    await message.answer("Вы отписались.")
