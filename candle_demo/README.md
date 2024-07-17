# CPU运行
```
cargo run --release -- --prompt your prompt
```

# Cuda运行
- 注意 需要cuda为>=12.4以上的版本
```
cargo build --release --features cuda
./target/release/codegeex4-candle --prompt your prompt
```
