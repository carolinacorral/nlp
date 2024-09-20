#include "toke.h"


int main() {
    std::setlocale(LC_ALL, "");


    std::wstring text = L"Este es un texto para ááá tokenización";
    std::vector<std::wstring> ans = tokenize(text);

    for (int i = 0; i < ans.size(); i++) {
        std::wcout << ans[i] << std::endl;
    }

    return 0;
}
