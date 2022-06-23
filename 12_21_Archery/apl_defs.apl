⍝ This doesn't solve anything, just simulates the game.

bots ← 'Aaron' 'Barron' 'Caren' 'Darrin'

archery ← {                             
     (≢⍵)=1:⍵ ⋄               
     ⍺←1                      
     newShot←?0               
     newShot<⍺:newShot ∇ 1⌽⍵ ⋄
     ⍺ ∇ 1↓⍵                  
 }      
 
playRounds ← {{⍵[⍋⍵;]}{⍺(≢⍵)}⌸(↑↑(⍵⍴1)archery¨⊂bots)}
 
 
