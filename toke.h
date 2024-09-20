#include <stdio.h>
#include <iostream>
#include <vector>
#include <string>
#include <locale> 

#pragma once

// prototypes
std::vector<std::wstring> tokenize(const std::wstring& text);
void to_lower(const std::wstring& word);
bool is_sc(wchar_t letter);
bool is_alpha(wchar_t letter);
bool is_space(wchar_t c);
bool is_stopword(const std::wstring word);

bool is_sc(wchar_t letter) {
    // special characters 
    std::vector<wchar_t> sc = {L'Á', L'É', L'Í', L'Ó', L'Ú', L'á', L'é', L'í', L'ó', L'ú'};
    int l = 0;
    int r = sc.size() - 1;
    int mid;

    // binary search
    while (l <= r) {
        mid = (l + r) / 2;
        if (sc[mid] == letter) {
            return true;
        } else if (letter < sc[mid]) {
            r = mid - 1;
        } else {
            l = mid + 1;
        }
    }

    return false;
}


bool is_alpha(wchar_t letter) {
    if (L'A' <= letter && letter <= L'Z') {
        return true;
    } else if (L'a' <= letter && letter <= L'z') {
        return true;
    } else {
        return false;
    }
}

bool is_space(wchar_t c) {
    if (c == L' ') {
        return true;
    } else {
        return false;
    }
}

std::vector<std::wstring> tokenize(std::wstring& text) {
    int i = 0;
    int n = text.length();
    std::vector<std::wstring> tokens;
    std::wstring curr;

    while (i < n) {
        if (is_sc(text[i]) || is_alpha(text[i])) {
            curr.push_back(text[i]);
        } else if (is_space(text[i])) {
            if (curr.size() > 0) {
                tokens.push_back(curr);
                curr = L"";  
            }
        }
        i++;
    }

    if (curr.size() > 0) {
        tokens.push_back(curr);
    }

    return tokens;
}


void to_lower(std::wstring& word) {
    for (int i = 0; i < word.size(); i++) {
        if (L'A' <= word[i] && word[i] <= L'Z') {
            word[i] = word[i] + (L'a' - L'A');  
        }
    }
}

bool is_stopword(std::wstring word){
    ///
}
