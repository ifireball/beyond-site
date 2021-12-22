function! myspacevim#before() abort
  let g:neoformat_python_isort = {
      \ 'exe': 'isort',
      \ 'stdin': 1,
      \ 'args': ['--profile', 'black', '-'],
      \ }
  let g:neoformat_python_black = {
      \ 'exe': 'black',
      \ 'stdin': 1,
      \ 'args': ['-q', '-'],
      \ }
  let g:neoformat_enabled_python = ['isort', 'black']
  let g:neoformat_run_all_formatters = 1
endfunction

function! myspacevim#after() abort
  let test#python#pytest#file_pattern = "^(tests\.py|test_.*\.py|.*_tests\.py)$"
endfunction
