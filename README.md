<!--
  Images in assets/ are generated, not hand-made:
  - SVGs (hero, tiles, buttons, trophies): python3 tools/build_assets.py
  - 3D GIF tiles (rubish, Town Trial, Multivis):            python3 tools/build_gifs.py
  - narrow banner + social buttons (logos in tools/logos/): python3 tools/trial_assets.py && python3 tools/build_social.py
  Edit the scripts, re-run them, and commit the new files in assets/.

  Layout rules (keep these or the edges stop lining up):
  - Every grid row spans exactly 0-100%: 32% column + 1.99% gap + 32% + 1.99% + 32%.
    Gaps are transparent spacer images, NOT spaces, so images in a row must sit on one
    line with no whitespace between them (a space's width depends on the viewer's font).
  - A Demo/Video pair is two 16% halves (tools/build_assets.py demo_button side=...).
  - Header: GitHub adds 20px padding to the inner side of align=left/right images, so
    the banner's left edge and the socials' right edge land exactly on 0% and 100%.
    Banner 76.63% / socials 8.8% keeps their heights equal and fits down to ~275px wide.
-->

<p>
  <img src="assets/hero-narrow.svg" width="76.63%" align="left" alt="SMARAN. CS + Math at UC Berkeley.">
  <a href="https://www.linkedin.com/in/smaran-kudapa/"><img src="assets/btn-social-linkedin.png" width="8.8%" align="right" alt="LinkedIn"></a>
  <br clear="right">
  <a href="https://www.youtube.com/@smarankudapa591"><img src="assets/btn-social-youtube.png" width="8.8%" align="right" alt="YouTube"></a>
  <br clear="right">
  <a href="https://x.com/KudapaSmaran"><img src="assets/btn-social-x.png" width="8.8%" align="right" alt="X"></a>
  <br clear="all">
</p>

<p align="center">
  <a href="https://github.com/SmaranKudapa/rubish"><img src="assets/tile-rubish.gif" width="32%" alt="rubish: turn a word into Rubik's cube moves that spell it. (repo)"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://github.com/SmaranKudapa/town-trial"><img src="assets/tile-town-trial.gif" width="32%" alt="Town Trial: research agents test local policy in a simulated town. (repo)"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://github.com/SmaranKudapa/picky"><img src="assets/tile-picky.svg" width="32%" alt="picky: everyone agrees on food. 2nd place, Hack With Claude. (repo)"></a>
  <br>
  <a href="https://rubish-delta.vercel.app"><img src="assets/btn-demo-rubish.svg" width="32%" alt="rubish demo"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://town-trial.vercel.app"><img src="assets/btn-demo-town-trial.svg" width="16%" alt="Town Trial demo"></a><a href="https://www.youtube.com/watch?v=ZaJVsbZ8RjM"><img src="assets/btn-video-town-trial.svg" width="16%" alt="Town Trial video"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://picky-ten-flax.vercel.app"><img src="assets/btn-demo-picky.svg" width="16%" alt="picky demo"></a><a href="https://www.youtube.com/shorts/55nvBi-CMXI"><img src="assets/btn-video-picky.svg" width="16%" alt="picky video"></a>
</p>

<p align="center">
  <a href="https://github.com/SmaranKudapa/claimos"><img src="assets/tile-claimos.svg" width="32%" alt="Claim OS: AI agents that appeal your property taxes. 4th place, YC x Naive Hackathon. (repo)"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://github.com/SmaranKudapa/multivis"><img src="assets/tile-multivis.gif" width="32%" alt="Multivis: see double and triple integrals in 3D. (repo)"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://github.com/SmaranKudapa/tempest"><img src="assets/tile-tempest.svg" width="32%" alt="Tempest: live indoor climate from an Arduino sensor. (repo)"></a>
  <br>
  <a href="https://claimos-site-mds8vwd4myby.vercel.app/"><img src="assets/btn-demo-claimos.svg" width="16%" alt="Claim OS demo"></a><a href="https://www.youtube.com/watch?v=f6ASmuaO4IY"><img src="assets/btn-video-claimos.svg" width="16%" alt="Claim OS video"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://smarankudapa.github.io/multivis/"><img src="assets/btn-demo-multivis.svg" width="32%" alt="Multivis demo"></a><img src="assets/spacer.svg" width="1.99%" alt=""><img src="assets/spacer.svg" width="32%" alt="">
</p>

<p align="center">
  <a href="https://github.com/SmaranKudapa/picky"><img src="assets/award-picky.svg" width="49%" alt="2nd place, Hack With Claude at UC Berkeley, for picky"></a><img src="assets/spacer.svg" width="1.99%" alt=""><a href="https://github.com/SmaranKudapa/claimos"><img src="assets/award-claimos.svg" width="49%" alt="4th place at the YC x Naive Hackathon, for Claim OS"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/smaran-kudapa/"><img src="assets/btn-continue.svg" width="280" alt="Continue on LinkedIn"></a>
</p>
