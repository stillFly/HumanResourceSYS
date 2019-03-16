set nocompatible
filetype off

"set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'gmarik/Vundle.vim'
Plugin 'tmhedberg/SimpylFold'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'scrooloose/syntastic'
Plugin 'nvie/vim-flake8'
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'

" comment
Plugin 'scrooloose/nerdcommenter'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'

" use git in vim
Plugin 'tpope/vim-fugitive'
Plugin 'Lokaltog/powerline',{'rtp': 'powerline/bindings/vim/'}
Plugin 'davidhalter/jedi-vim'
Plugin 'ervandew/supertab'

call vundle#end()
filetype plugin indent on

set encoding=utf-8
set nu
set cursorline
set hlsearch

set splitbelow
set splitright

" split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Enable folding
set foldmethod=indent
set foldlevel=99

" Enable folding with the spacebar
nnoremap <space> za

" doc string present
let g:SimpylFold_docstring_preview=1

let python_highlight_all=1
syntax on

colorscheme solarized
if has('gui_running')
    set background=light
else
    set background=dark
endif

call togglebg#map("<F2>")

" NERDTree settings
let NERDTreeIgnore=['\.pyc$', '\~$']
"let NERDTreeShowLineNumbers=1
let g:nerdtree_tabs_open_on_gui_startup = 1
let g:nerdtree_tabs_open_on_console_startup = 1
"let g:nerdtree_tabs_no_startup_for_diff = 1
"let g:nerdtree_tabs_smart_startup_focus = 1

"au BufNewFile,BufRead *.js, *.html, *.css
"\ set tabstop=2
"\ set softtabstop=2
"\ set shiftwidth=2

" python with virtualenv support
py << EOF
import os
import sys
if 'VIRTUAL_ENV' in os.environ:
	project_base_dir = os.environ['VIRTUAL_ENV']
	activate_this = os.path.join(project_base_dir, 'bin/activate_this.py')
	execfile(activate_this, dict(__file__=activate_this))
EOF

map <F5> : call CompileRunGcc()<CR>
func! CompileRunGcc()
	exec "w"
if &filetype == 'c'
	exec "!g++ % -o %<"
	exec "!time ./%<"
elseif &filetype == 'cpp'
	exec "!g++ % -o %<"
	exec "!time ./%<"
elseif &filetype == 'java'
	exec "!javac %"
	exec "!time java %<"
elseif &filetype == 'sh'
	:!time bash%
elseif &filetype == 'python'
	exec "!time python %"
endif
endfunc
