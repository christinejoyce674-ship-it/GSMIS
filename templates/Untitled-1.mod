<label>Session Year</label>
<select class="form-control" name="session_year_id" required>
    <option>Select Session Year</option>
    {% for i in sessions %}
    <option value="{{i.id}}">{{i.session_start}} to {{i.session_end}}</option>
    {% endfor %}
</select>