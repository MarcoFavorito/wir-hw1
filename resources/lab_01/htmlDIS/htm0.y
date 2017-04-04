/*
 * Parser per miniHTML, versione 1
 * (da usare insieme all'analizzatore lessicale realizzato con FLEX
 *  a partire da htm0.fl).
 *
 * Sequenza di comandi per generare il parser:
 *
 *     flex htm0.fl
 *     bison -d htm0.y
 *     PER DOS/WINDOWS: gcc lexyy.c htm0_tab.c -lfl -o mini0
 *     PER LINUX/UNIX: gcc lex.yy.c htm0.tab.c -lfl -o mini0
 *
 * Richiamare il parser tramite il comando:
 *
 *     mini0 < nomefileinput
 *
 * oppure ridirigendo l'output su un file:
 *
 *     mini0 < nomefileinput > nomefileoutput
 */

%{
#include<string.h>
#include<stdlib.h>
%}

/*** Dichiarazione di tutti i token terminali riconosciuti da flex  ***/

%token Shtml Ehtml Shead Ehead Sbody Ebody Stitle Etitle Sol Eol Sul Eul Sh1 Eh1 Sh2 Eh2 Sh3 Eh3 Sh4 Eh4 Sh5 Eh5 Sh6 Eh6 Sb Eb Si Ei Scenter Ecenter Hr Br Sp  Text Sli Eli Sem Eem Scode Ecode Sdd Edd 

%start html_document

%%
html_document : Shtml html_content Ehtml ;

html_content : head_tag body_tag ;

head_tag : Shead lista_head_content Ehead ;

lista_head_content : lista_head_content head_content | ;

head_content : title_tag ;

title_tag : Stitle Text Etitle ;
 
body_tag : Sbody lista_body_content Ebody ;

lista_body_content : lista_body_content body_content | ;

body_content : hr_tag | block | heading | text_content ;
 
hr_tag : Hr ;

block : block_content lista_block_content ;

lista_block_content : lista_block_content block_content | ;

block_content : ol_tag | ul_tag | center_tag ;

ol_tag : Sol lista_li_tag Eol ;

ul_tag : Sul lista_li_tag Eul ;

lista_li_tag : lista_li_tag li_tag | ;

li_tag : Sli lista_flow_content Eli ;

lista_flow_content : lista_flow_content flow_content | ;

flow_content : block | block_text ;

center_tag : Scenter lista_body_content Ecenter ;

heading : h1_tag | h2_tag | h3_tag | h4_tag | h5_tag | h6_tag ;

h1_tag : Sh1 block_text Eh1 ;

h2_tag : Sh2 block_text Eh2 ;

h3_tag : Sh3 block_text Eh3 ;

h4_tag : Sh4 block_text Eh4 ;

h5_tag : Sh5 block_text Eh5 ;

h6_tag : Sh6 block_text Eh6 ;

block_text : lista_text_content ;

lista_text_content : lista_text_content text_content | ;

text_content : Text | Br | Sp | code_tag | em_tag | b_tag | 
               i_tag  | dd_tag ;

code_tag : Scode block_text Ecode ;

em_tag : Sem block_text Eem ;

b_tag : Sb block_text Eb ;

i_tag : Si block_text Ei ;

dd_tag : Sdd block_text Edd ;


%%

yyerror (s)  /* Called by yyparse on error */
     char *s;
	{
      printf ("%s\n", s);
    
}

main ()
{ 
 yyparse (); 
}





