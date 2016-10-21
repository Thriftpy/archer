exception PingPongException {
    1: required i32 error_code,
    2: required string error_name,
    3: optional string message,
}

service PingPong {
    string ping(),
    string get(1:string id),
    string mget(1:i32 id),
    void set_v(1:string k, 2:string v),
    string query(1:string id)
    string health_check(1:string id)
        throws (1:PingPongException exc)
}

