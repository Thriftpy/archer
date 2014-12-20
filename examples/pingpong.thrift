service PingPong {
    string ping(),
    i32 get(1:i32 id),
    string mget(1:i32 id),
    string redis_get(1:string k),
    void redis_set(1:string k, 2:string v),

    string fuck_api()


}