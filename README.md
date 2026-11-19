# Upscaling Job Routing Output Size

This example demonstrates why routing upscaling jobs based on input file size can be misleading, and why output size (or estimated processing cost) is a more reliable metric. It simulates several upscaling jobs, calculating their input/output dimensions and a derived processing cost. The script then compares two routing strategies: one based on input pixels and another based on processing cost, highlighting how the naive input-based approach can misallocate computationally intensive tasks.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Upscaling İşlerini Çıktı Boyutuna Göre Yönlendirmek: Neden Giriş Boyutu Yanıltıcı Olabilir?](https://fatihsoysal.com/blog/upscaling-islerini-cikti-boyutuna-gore-yonlendirmek-neden-giris-boyutu-yaniltici-olabilir/).

## License

MIT — see [LICENSE](LICENSE).
