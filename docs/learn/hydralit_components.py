import hydralit_components as hc
import streamlit as st


hc.hydralit_experimental(True)


modal_code = """
<div>
<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
Hydralit Components Experimental Demo!
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog" role="document">
<div class="modal-content">
<div class="modal-header">
  <h5 class="modal-title" id="exampleModalLabel">Modal Popup Form!</h5>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
<div class="modal-body">
  <div class="container">
<h2>Pure JS+HTML Form</h2>
<form class="form-horizontal" action="/">
<div class="form-group">
<label class="control-label col-sm-2" for="email">Email:</label>
<div class="col-sm-10">
  <input type="email" class="form-control" id="email" placeholder="Enter email" name="email">
</div>
</div>
<div class="form-group">
<label class="control-label col-sm-2" for="pwd">Password:</label>
<div class="col-sm-10">          
  <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="pwd">
</div>
</div>
<div class="form-group">        
<div class="col-sm-offset-2 col-sm-10">
  <div class="checkbox">
    <label><input type="checkbox" name="remember"> Remember me</label>
  </div>
</div>
</div>
<div class="form-group">        
<div class="col-sm-offset-2 col-sm-10">
  <button type="submit" class="btn btn-default">Submit</button>
</div>
</div>
</form>
</div>
</div>
<div class="modal-footer">
  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
  <button type="button" class="btn btn-primary">Save changes</button>
</div>
</div>
</div>
</div>
</div>
"""


st.markdown(modal_code,unsafe_allow_html=True)
query_param = st.experimental_get_query_params()

if query_param:
    st.write('We caputred these values from the experimental modal form using Javascript + HTML + Streamlit + Hydralit Components.')
    st.write(query_param)
