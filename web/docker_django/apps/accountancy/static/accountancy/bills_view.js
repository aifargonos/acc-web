

google.charts.load('current', {packages: ['corechart']});


class Bill {
  
  constructor(account, date, currency, items) {
    this.account = account
    this.date = date
    this.currency = currency
    this.items = items
  }
  
  total() {
    var result = 0
    for (var item_id in this.items) {
      const item = this.items[item_id]
      result += item.price()
    }
    return result
  }
  
}


class Item {
  
  constructor(category, name, comment, amount, unit, unit_price) {
    this.category = category
    this.name = name
    this.comment = comment
    this.amount = amount
    this.unit = unit
    this.unit_price = unit_price
  }
  
  price() {
    return this.amount * this.unit_price
  }
  
}


class BillList {
  
  constructor(bills) {
    this.bills = bills
    const sums = {}
    for (var bill_id in this.bills) {
      const bill = this.bills[bill_id]
      bill.id = bill_id
      for (var item_id in bill.items) {
        const item = bill.items[item_id]
        item.id = item_id
        item.bill = bill
        if (sums.hasOwnProperty(item.category)) {
          sums[item.category] += item.price()
        } else {
          sums[item.category] = item.price()
        }
      }
    }
    this.selected_bill_count = Object.keys(this.bills).length
    
    // children
    this.sums_table = new _SumsTable(sums)
    this.select_button = new _SelectButton(this)
    
    this.element = document.createElement("div")
    
    // render
    
    this.element.appendChild(this.sums_table.element)
    
    this.element.appendChild(document.createElement("br"))
    
    const bill_table = document.createElement("table")
    bill_table.border = 1
    bill_table.style['border-collapse'] = 'collapse'
    this.element.appendChild(bill_table)
    
    const header_row = document.createElement("tr")
    bill_table.appendChild(header_row)
    
    const select_col = document.createElement("th")
    select_col.appendChild(this.select_button.element)
    header_row.appendChild(select_col)
    
    const expand_col = document.createElement("th")
    header_row.appendChild(expand_col)
    
    const account_col = document.createElement("th")
    account_col.innerHTML = "account"
    header_row.appendChild(account_col)
    
    const date_col = document.createElement("th")
    date_col.innerHTML = "date"
    header_row.appendChild(date_col)
    
    const currency_col = document.createElement("th")
    currency_col.innerHTML = "currency"
    header_row.appendChild(currency_col)
    
    const total_col = document.createElement("th")
    total_col.innerHTML = "total"
    header_row.appendChild(total_col)
    
    const selected_total_col = document.createElement("th")
    selected_total_col.innerHTML = "selected total"
    header_row.appendChild(selected_total_col)
    
    const ids = Object.keys(this.bills)
    ids.sort(function(id1, id2) {
      const compare1 = "" + bills[id1].date
      const compare2 = "" + bills[id2].date
      var result = 0
      if (compare1 < compare2) {
        result = 1
      } else if (compare1 > compare2) {
        result = -1
      }
      return result
    })
    
    for (var i = 0; i < ids.length; i++) {
      const bill_id = ids[i]
      const bill = this.bills[bill_id]
      
      const bill_component = new _BillComponent(bill, this)
      bill_component.select_button.addOnSelectionChangedListener(this)
      bill_table.appendChild(bill_component.element)
      
      bill_table.appendChild(bill_component.item_list.element)
      
    }
    
  }
  
  onSelectionChanged(select_button) {
    if (select_button.isSelected()) {
      this.selected_bill_count += 1
    } else {
      this.selected_bill_count -= 1
    }
    // console.log('  this.selected_items_count=' + this.selected_items_count)
    
    if (this.selected_bill_count <= 0) {
      // console.log('  uncheck')
      this.select_button.element.indeterminate = false
      this.select_button.setSelectedAndFireEvent(false)
    } else if (this.selected_bill_count >= Object.keys(this.bills).length) {
      // console.log('  check')
      this.select_button.element.indeterminate = false
      this.select_button.setSelectedAndFireEvent(true)
    } else {
      // console.log('  indeterminate')
      this.select_button.element.indeterminate = true
    }
  }
  
}


class _SumsTable {
  
  constructor(sums) {
    this.sums = sums
    this.sum = 0
    
    this.element = document.createElement("div")
    
    // children
    this.sum_components = {}
    
    // render
    
    this.plot_div = document.createElement("div")
    this.plot_div.style.float = 'right'
    this.plot_div.style.width = '700px'
    this.element.appendChild(this.plot_div)
    
    const sums_table = document.createElement("table")
    sums_table.border = 1
    sums_table.style['border-collapse'] = 'collapse'
    this.element.appendChild(sums_table)
    
    for (var category in this.sums) {
      this.sum += this.sums[category]
      
      const row = document.createElement("tr")
      sums_table.appendChild(row)
      
      const category_col = document.createElement("th")
      category_col.style['text-align'] = 'left'
      category_col.innerHTML = category
      row.appendChild(category_col)
      
      const sum_col = document.createElement("td")
      sum_col.style['text-align'] = 'right'
      sum_col.innerHTML = _formatPrice(this.sums[category])
      row.appendChild(sum_col)
      
      this.sum_components[category] = sum_col
    }
    
    const row = document.createElement("tr")
    sums_table.appendChild(row)
    
    const category_col = document.createElement("th")
    category_col.innerHTML = 'sum'
    row.appendChild(category_col)
    
    this.sum_col = document.createElement("td")
    this.sum_col.style['text-align'] = 'right'
    this.sum_col.innerHTML = _formatPrice(this.sum)
    row.appendChild(this.sum_col)
    
    const this_sums_table = this
    google.charts.setOnLoadCallback(function() { this_sums_table.drawPlot() })
    
  }
  
  onSelectionChanged(select_button) {
    if (select_button.parent.constructor.name != _ItemComponent.name) {
      return
    }
    // else
    const category = select_button.parent.item.category
    const price = select_button.parent.item.price()
    if (select_button.isSelected()) {
      this.sums[category] += price
      this.sum += price
    } else {
      this.sums[category] -= price
      this.sum -= price
    }
    this.sum_components[category].innerHTML = _formatPrice(this.sums[category])
    this.sum_col.innerHTML = _formatPrice(this.sum)
    
    this.drawPlot()
  }
  
  drawPlot() {
    
    const plot = new google.visualization.ColumnChart(this.plot_div);
    const options = { legend: { position: "none" } }
    
    var data = [ ['category', 'sum', { role: 'style' }] ]
    for (var category in this.sums) {
      // round it to 2 decimal places to avoid float errors
      const s = Math.round(this.sums[category] * 100) / 100
      if (s < 0) {
        data = data.concat([ [category, -s, 'red'] ])
      } else {
        data = data.concat([ [category, s, 'green'] ])
      }
    }
    
    plot.draw(google.visualization.arrayToDataTable(data), options)
    
  }
  
}


class _BillComponent {
  
  constructor(bill, bill_list) {
    this.bill = bill
    this.expanded = false
    this.selected_items_count = Object.keys(this.bill.items).length
    // console.log('  this.selected_items_count=' + this.selected_items_count)
    
    // parent
    this.bill_list = bill_list
    
    this.element = document.createElement("tr")
    
    // children
    this.select_button = new _SelectButton(this)
    this.expand_button = new _ExpandButton(this)
    
    this.item_list = new _ItemList(bill.items, this)
    for (var i = 0; i < this.item_list.item_components.length; i++) {
      const item_component = this.item_list.item_components[i]
      item_component.select_button.addOnSelectionChangedListener(this)
    }
    
    this.selected_total_col = document.createElement("td")
    
    // render
    
    const select_col = document.createElement("td")
    select_col.appendChild(this.select_button.element)
    this.element.appendChild(select_col)
    
    const expand_col = document.createElement("td")
    this.element.appendChild(expand_col)
    expand_col.appendChild(this.expand_button.element)
    
    const account_col = document.createElement("td")
    account_col.innerHTML = this.bill.account
    this.element.appendChild(account_col)
    
    const date_col = document.createElement("td")
    // TODO: format this !!!
    date_col.innerHTML = this.bill.date
    this.element.appendChild(date_col)
    
    const currency_col = document.createElement("td")
    currency_col.innerHTML = this.bill.currency
    this.element.appendChild(currency_col)
    
    const total_col = document.createElement("td")
    total_col.style['text-align'] = 'right'
    total_col.innerHTML = _formatPrice(this.bill.total())
    this.element.appendChild(total_col)
    
    this.selected_total_col.style['text-align'] = 'right'
    this.selected_total_col.innerHTML = _formatPrice(this.item_list.selectedTotal())
    this.element.appendChild(this.selected_total_col)
    
    const this_bill_component = this
    this.bill_list.select_button.addOnSelectionChangedListener({
      onSelectionChanged: function(select_button) {
        this_bill_component.select_button.setSelectedAndFireEvent(select_button.isSelected())
      }
    })
    
  }
  
  onSelectionChanged(select_button) {
    // console.log('_BillComponent.onSelectionChanged this.bill.id=' + this.bill.id)
    if (select_button.isSelected()) {
      this.selected_items_count += 1
    } else {
      this.selected_items_count -= 1
    }
    // console.log('  this.selected_items_count=' + this.selected_items_count)
    
    if (this.selected_items_count <= 0) {
      // console.log('  uncheck')
      this.select_button.element.indeterminate = false
      this.select_button.setSelectedAndFireEvent(false)
    } else if (this.selected_items_count >= Object.keys(this.bill.items).length) {
      // console.log('  check')
      this.select_button.element.indeterminate = false
      this.select_button.setSelectedAndFireEvent(true)
    } else {
      // console.log('  indeterminate')
      this.select_button.element.indeterminate = true
    }
    
    this.selected_total_col.innerHTML = _formatPrice(this.item_list.selectedTotal())
  }
  
}


class _ExpandButton {
  
  constructor(bill_component) {
    // parent
    this.bill_component = bill_component
    
    this.onClickListeners = [this]
    
    this.element = document.createElement("input")
    this.element.type = 'button'
    this.element.value = '+'
    const this_button = this
    this.element.onclick = function() {this_button.onClick()}
  }
  
  onClick() {
    // console.log('_ExpandButton.onClick this.bill.id=' + this.bill.id)
    const this_button = this
    this.onClickListeners.forEach(function(listener) {
      // console.log('  calling listener listener.constructor.name=' + listener.constructor.name)
      listener.expandButtonOnClick(this_button)
    })
  }
  
  expandButtonOnClick(expandButton) {
    // console.log('_ExpandButton.expandButtonOnClick expandButton.bill.id=' + expandButton.bill.id)
    if (expandButton.bill_component.expanded) {
      expandButton.bill_component.expanded = false
      expandButton.element.value = '+'
    } else {
      expandButton.bill_component.expanded = true
      expandButton.element.value = '-'
    }
  }
  
  addOnClickListener(listener) {
    // console.log('_ExpandButton.addOnClickListener this.bill.id=' + this.bill.id + ' listener.constructor.name=' + listener.constructor.name)
    this.onClickListeners = this.onClickListeners.concat(listener)
  }
  
}


class _ItemList {
  
  constructor(items, bill_component) {
    this.items = items
    
    // parent
    this.bill_component = bill_component
    
    this.element = document.createElement("tr")
    
    this.bill_component.expand_button.addOnClickListener(this)
    
    // children
    this.item_components = []
    for (var item_id in this.items) {
      const item = this.items[item_id]
      const item_component = new _ItemComponent(item, this)
      this.item_components = this.item_components.concat(item_component)
      this.bill_component.select_button.addOnSelectionChangedListener(item_component)
    }
    
  }
  
  expandButtonOnClick(expandButton) {
    // console.log('_ItemList.expandButtonOnClick expandButton.bill.id=' + expandButton.bill.id)
    if (expandButton.bill_component.expanded) {
      this._renderItems()
    } else {
      this.element.innerHTML = ''
    }
  }
  
  _renderItems() {
    const item_table_col = document.createElement("td")
    item_table_col.colSpan = 7
    this.element.appendChild(item_table_col)
    const item_table = document.createElement("table")
    item_table.border = 1
    item_table.style['border-collapse'] = 'collapse'
    item_table.align = 'right'
    item_table_col.appendChild(item_table)
    
    for (var i = 0; i < this.item_components.length; i++) {
      const item_component = this.item_components[i]
      item_table.appendChild(item_component.element)
    }
    
  }
  
  selectedTotal() {
    // console.log('_ItemList.selectedTotal')
    var result = 0
    for (var i = 0; i < this.item_components.length; i++) {
      const item_component = this.item_components[i]
      if (item_component.isSelected()) {
        result += item_component.item.price()
      }
    }
    return result
  }
  
}


class _ItemComponent {
  
  constructor(item, item_list) {
    this.item = item
    
    // parent
    this.item_list = item_list
    
    this.element = document.createElement("tr")
    
    // children
    this.select_button = new _SelectButton(this)
    this.select_button.addOnSelectionChangedListener(this.item_list.bill_component.bill_list.sums_table)
    
    // render
    
    const item_select_col = document.createElement("td")
    item_select_col.appendChild(this.select_button.element)
    this.element.appendChild(item_select_col)
    
    const category_col = document.createElement("td")
    category_col.innerHTML = item.category
    this.element.appendChild(category_col)
    
    const name_col = document.createElement("td")
    name_col.innerHTML = item.name
    this.element.appendChild(name_col)
    
    const comment_col = document.createElement("td")
    comment_col.innerHTML = item.comment
    this.element.appendChild(comment_col)
    
    const amount_col = document.createElement("td")
    amount_col.style['text-align'] = 'right'
    amount_col.innerHTML = item.amount
    this.element.appendChild(amount_col)
    
    const unit_col = document.createElement("td")
    unit_col.innerHTML = item.unit
    this.element.appendChild(unit_col)
    
    const unit_price_col = document.createElement("td")
    unit_price_col.style['text-align'] = 'right'
    unit_price_col.innerHTML = _formatPrice(item.unit_price)
    this.element.appendChild(unit_price_col)
    
    const price_col = document.createElement("td")
    price_col.style['text-align'] = 'right'
    price_col.innerHTML = _formatPrice(item.price())
    this.element.appendChild(price_col)
    
  }
  
  isSelected() {
    const result = this.select_button.isSelected()
    // console.log('_ItemComponent.isSelected = ' + result)
    return result
  }
  
  onSelectionChanged(select_button) {
    this.select_button.setSelectedAndFireEvent(select_button.isSelected())
  }
  
}


class _SelectButton {
  
  constructor(parent) {
    this.parent = parent
    
    this.onSelectionChangedListeners = []
    
    this.element = document.createElement("input")
    this.element.type = 'checkbox'
    this.element.checked = true
    const this_button = this
    this.element.onclick = function() {this_button.fireSelectionChanged()}
  }
  
  fireSelectionChanged() {
    // console.log('_SelectButton.fireSelectionChanged')
    const this_button = this
    this.onSelectionChangedListeners.forEach(function(listener) {
      // console.log('  calling listener listener.constructor.name=' + listener.constructor.name)
      listener.onSelectionChanged(this_button)
    })
  }
  
  isSelected() {
    // console.log('_SelectButton.isSelected = ' + this.element.checked)
    return this.element.checked
  }
  
  setSelectedAndFireEvent(selected) {
    const old_selected = this.element.checked
    this.element.checked = selected
    if (old_selected != this.element.checked) {
      this.fireSelectionChanged()
    }
  }
  
  addOnSelectionChangedListener(listener) {
    // console.log('_SelectButton.addOnSelectionChangedListener listener.constructor.name=' + listener.constructor.name)
    this.onSelectionChangedListeners = this.onSelectionChangedListeners.concat(listener)
  }
  
}


function _formatPrice(price) {
  // TODO: also ensure 2 decimal places!
  return price.toFixed(2)
}


